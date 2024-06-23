import React, { useRef, useState } from "react";

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
  return (
    <dialog ref={ref} id="seed_modal" className="modal">
      <div className="modal-box">
        <h3 className="font-bold text-center text-lg mb-4">
          Seed your database
        </h3>
        <ul className="steps w-full text-xs">
          <li className="step step-primary">Analyze Schema</li>
          <li className="step step-primary">Generate Data</li>
          <li className="step">Seed Database</li>
        </ul>
      </div>
      <form method="dialog" className="modal-backdrop">
        <button></button>
      </form>
    </dialog>
  );
}
