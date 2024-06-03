import { atom } from "nanostores";

export const $env = atom({
  baseUrl: import.meta.env.VITE_TWEAKED_API,
});
