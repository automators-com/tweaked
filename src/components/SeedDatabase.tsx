import React, { useRef, useState } from "react";
import { $baseUrl, $connection, $schema } from "@/store/config";
import { useStore } from "@nanostores/react";
import toast from "react-hot-toast";

export default function SeedDatabase() {
  const ref = useRef(null);

  return (
    <>
      <button
        type="button"
        onClick={() => {
          if (ref.current !== null) {
            // @ts-ignore
            ref.current?.showModal();
          }
        }}
        className="btn btn-sm text-xs btn-block btn-ghost justify-start"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          className="size-4"
          viewBox="0 0 256 256"
        >
          <path d="M205.41,159.07a60.9,60.9,0,0,1-31.83,8.86,71.71,71.71,0,0,1-27.36-5.66A55.55,55.55,0,0,0,136,194.51V224a8,8,0,0,1-8.53,8,8.18,8.18,0,0,1-7.47-8.25V211.31L81.38,172.69A52.5,52.5,0,0,1,63.44,176a45.82,45.82,0,0,1-23.92-6.67C17.73,156.09,6,125.62,8.27,87.79a8,8,0,0,1,7.52-7.52c37.83-2.23,68.3,9.46,81.5,31.25A46,46,0,0,1,103.74,140a4,4,0,0,1-6.89,2.43l-19.2-20.1a8,8,0,0,0-11.31,11.31l53.88,55.25c.06-.78.13-1.56.21-2.33a68.56,68.56,0,0,1,18.64-39.46l50.59-53.46a8,8,0,0,0-11.31-11.32l-49,51.82a4,4,0,0,1-6.78-1.74c-4.74-17.48-2.65-34.88,6.4-49.82,17.86-29.48,59.42-45.26,111.18-42.22a8,8,0,0,1,7.52,7.52C250.67,99.65,234.89,141.21,205.41,159.07Z"></path>
        </svg>
        Seed database
      </button>
      <SeedModal ref={ref} />
    </>
  );
}

function SeedModal({ ref }: { ref: any }) {
  const baseUrl = useStore($baseUrl);
  const connection = useStore($connection);
  const [schema, setSchema] = useState<string>("");
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);

  async function handleSeed() {
    setLoading(true);
    setCurrentStep(1);

    // analyze database
    console.log("Analyzing database...");
    if (!schema) {
      const res = await fetch(`${baseUrl}/schema`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          connection_string: connection,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          setCurrentStep(2);
          if (data.schema) {
            return data.schema;
          }
        })
        .catch((err) => {
          console.error(err);
          setCurrentStep(0);
          setLoading(false);
          return false;
        });

      console.log({ res });
      setSchema(res);
      if (!res) {
        toast.error("Failed to analyze schema");
        return;
      }

      // generate data
      console.log("Generating data...");
      setCurrentStep(3);

      await fetch(`${baseUrl}/data/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          connection_string: connection,
          db_schema: res,
          quantities: 10,
        }),
      })
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            throw new Error("Failed to generate data");
          }
        })
        .then((data) => {
          console.log(data);
          setCurrentStep(4);
          toast.success("Database seeded successfully");
          setLoading(false);
        })
        .catch((err) => {
          console.error(err);
          setCurrentStep(2);
          toast.error("Failed to generate data");
          setLoading(false);
        });
    }
  }

  return (
    <dialog ref={ref} id="seed_modal" className="modal">
      <div className="modal-box">
        <h3 className="font-bold text-center text-lg mb-4">
          Seed your database
        </h3>
        <ul className="steps w-full text-xs transition-all duration-500">
          <li className={`step ${currentStep >= 1 ? `step-primary` : ``}`}>
            {currentStep == 1 ? `Analyzing schema` : `Analyze Schema`}
          </li>
          <li className={`step ${currentStep >= 2 ? `step-primary` : ``}`}>
            {currentStep == 2 ? `Generating Data` : `Generate Data`}
          </li>
          <li className={`step ${currentStep >= 3 ? `step-primary` : ``}`}>
            {currentStep == 3 ? `Seeding...` : `Seed Database`}
          </li>
        </ul>
        <div className="modal-action">
          <button
            type="button"
            className="btn btn-sm btn-primary"
            disabled={loading}
            onClick={async () => {
              await handleSeed();
            }}
          >
            {loading ? (
              <span className="loading loading-spinner text-accent"></span>
            ) : (
              `Start`
            )}
          </button>
        </div>
      </div>
      <form method="dialog" className="modal-backdrop">
        <button></button>
      </form>
    </dialog>
  );
}
