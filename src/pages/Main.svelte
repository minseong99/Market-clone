<script>
  import { onMount } from "svelte";

  import { getDatabase, ref, onValue } from "firebase/database";
  import Nav from "../components/Nav.svelte";

  let hour = new Date().getHours();
  let min = new Date().getMinutes();

  // $: items : items가 반응형 변수로 선언이 된다. 즉, items의 값이 바뀌게 되면  html부분에서 items를 랜더링하고있는 태그에서
  //             자동으로 값이 바뀌면 화면이 바뀐다.
  $: items = [];

  const calcTime = (timeStamp) => {
    // 한국시간 UTC + 9
    const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
    const passedTime = new Date(curTime - timeStamp);
    const hours = passedTime.getHours();
    const minutes = passedTime.getMinutes();
    const seconds = passedTime.getSeconds();
    const months = passedTime.getMonth();
    const days = passedTime.getDate();

    if (months > 0) return ` ${months}달 전`;
    else if (days > 1) return ` ${days}일 전`;
    else if (hours > 0) return ` ${hours}시간 전`;
    else if (minutes > 0) return ` ${minutes}분 전`;
    else if (seconds > 0) return ` ${seconds}초 전`;
    else return "방금 전";
  };

  const db = getDatabase();
  const itemsRef = ref(db, "items/");
  // onValue : itemsRef를 받는데 itemsRef가 바뀔때마다 snapshot이 새롭게 내려온다.
  onMount(() => {
    onValue(itemsRef, (snapshot) => {
      const data = snapshot.val();
      //Object.values() : value들만 가져와서 array를 만들어준다
      items = Object.values(data).reverse();
    });
  });
</script>

<header>
  <div class="info-bar">
    <div class="info-bar__time">{hour}:{min}</div>
    <div class="info-bar__icons">
      <img src="assets/char-bar.svg" alt="chart-bar" />
      <img src="assets/wifi.svg" alt="wifi-bar" />
      <img src="assets/battery.svg" alt="battery-bar" />
    </div>
  </div>

  <div class="menu-bar">
    <div class="menu-bar__location">
      <div>역삼1동</div>
      <div class="menu-bar__location-icon">
        <img src="assets/arrow-down.svg" alt="arrow-down" />
      </div>
    </div>
    <div class="menu-bar__icons">
      <img src="assets/search.svg" alt="search" />
      <img src="assets/menu.svg" alt="menu" />
      <img src="assets/alert.svg" alt="alert" />
    </div>
  </div>
</header>

<main>
  {#each items as item}
    <div class="items-list">
      <div class="items-list__img">
        <img alt={item.title} src={item.imgUrl} />
      </div>
      <div class="items-list__info">
        <div class="items-list__info-title">{item.title}</div>
        <div class="items-list__info-meta">
          {item.place}
          {calcTime(item.insertAt)}
        </div>
        <div class="items-list__info-price">{item.price}</div>

        <div>{item.description}</div>
      </div>
    </div>
  {/each}
  <a class="write-btn" href="#/write">+ 글쓰기</a>
</main>

<Nav location="home" />

<div class="media-info-msg">
  <div class="media-info-msg-text">화면 사이즈를 줄여주세요.</div>
</div>
