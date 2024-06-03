import { persistentAtom } from "@nanostores/persistent";

type Previews = {
  id: string;
  table_name: string;
  table_row_count: number;
  preview: any[];
};

export const $previews = persistentAtom<Previews[]>("previews", [], {
  encode: (value) => JSON.stringify(value),
  decode: (value) => JSON.parse(value),
});
