import { writable } from "svelte/store";

//상태 관리를 위해, 현재 상태가 어떤지를 이 파일에 저장을 한다.

// writable은 수정할 수 있는 그런 값
export const user$ = writable(null);
