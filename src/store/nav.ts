import { atom } from "nanostores";

export const $nav = atom<{
  leftOpen: boolean;
  rightOpen: boolean;
}>({
  leftOpen: true,
  rightOpen: false,
});

export function toggleLeftNav() {
  $nav.set({
    leftOpen: !$nav.get().leftOpen,
    rightOpen: $nav.get().rightOpen,
  });
}

export function toggleRightNav() {
  $nav.set({
    leftOpen: $nav.get().leftOpen,
    rightOpen: !$nav.get().rightOpen,
  });
}
