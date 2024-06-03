import { persistentAtom } from "@nanostores/persistent";

export const $connection = persistentAtom<string>(
  "connection",
  "postgres://user:password@localhost:5432/dbname",
);

export const $baseUrl = persistentAtom<string>(
  "baseUrl",
  "http://localhost:8000",
);

export const $selectedTable = persistentAtom<string>("selectedTable", "");

export const $previewLimit = persistentAtom<number>("previewLimit", 10, {
  encode: (value) => value.toString(),
  decode: (value) => parseInt(value),
});
