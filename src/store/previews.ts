import { persistentAtom } from "@nanostores/persistent";

type Previews = {
  [table_name: string]: any[];
};

export const $previews = persistentAtom<Previews>(
  "previews",
  {},
  {
    encode: JSON.stringify,
    decode: JSON.parse,
  },
);
