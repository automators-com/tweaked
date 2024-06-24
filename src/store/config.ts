import { persistentAtom } from "@nanostores/persistent";

export enum Mode {
  SEED = "seed",
  TWEAK = "tweak",
  QUERY = "query",
}
export const $mode = persistentAtom<Mode>(Mode.TWEAK);

export const $fingerprint = persistentAtom<string | undefined>(
  "fingerprint",
  undefined,
);

export const $connection = persistentAtom<string>(
  "connection",
  "postgres://user:password@host:5432/dbname",
);

export const $baseUrl = persistentAtom<string>(
  "baseUrl",
  "https://tweaked.onrender.com",
);

export const $selectedTable = persistentAtom<string>("selectedTable", "");

export const $previewLimit = persistentAtom<number>("previewLimit", 10, {
  encode: (value) => value.toString(),
  decode: (value) => parseInt(value),
});

export const $schema = persistentAtom<string | undefined>("schema", undefined);
