import { persistentAtom } from "@nanostores/persistent";

export const connection = persistentAtom<string>(
  "connection",
  "postgres://user:password@localhost:5432/dbname",
);
