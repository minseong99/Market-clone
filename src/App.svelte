<script>
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Router from "svelte-spa-router";
  import "./css/style.css";
  import {
    GoogleAuthProvider,
    getAuth,
    signInWithCredential,
  } from "firebase/auth";
  import { user$ } from "./store";
  import { onMount } from "svelte";
  import Loding from "./pages/Loding.svelte";
  import Mypage from "./pages/Mypage.svelte";

  const auth = getAuth();

  //로그인 상태 일때 새로고침을 하면
  //로그인 화면이 잠깐 나왔다가
  //페이지로 가는것을 방지하기 위해 사용
  let isLoading = true;

  const checkLogin = async () => {
    const token = localStorage.getItem("token"); // access token
    if (!token) return (isLoading = false);
    const credential = GoogleAuthProvider.credential(null, token);
    const result = await signInWithCredential(auth, credential);
    const user = result.user;
    //store user정보 업데이트
    user$.set(user);
    isLoading = false;
  };

  const routes = {
    "/": Main,
    "/signup": Signup,
    "/write": Write,
    "/my": Mypage,
    "*": NotFound,
  };
  onMount(() => checkLogin());
</script>

{#if isLoading}
  <Loding />
{:else if !$user$}
  <Login />
{:else}
  <div class="user-name">{$user$.displayName}</div>
  <Router {routes} />
{/if}
