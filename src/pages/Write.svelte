<script>
  import { getDatabase, ref, push } from "firebase/database";
  import Footer from "../components/Footer.svelte";
  // 참조가 겹쳐서 ref를 refImage로 바꾸었다.
  import {
    getDownloadURL,
    getStorage,
    ref as refImage,
    uploadBytes,
  } from "firebase/storage";
  let title;
  let price;
  let description;
  let place;
  let files;

  const storage = getStorage();
  const db = getDatabase();

  // 반응형으로 files가 바뀔때마다 console.log(files)가 찍히게 된다.
  // $: if (files) console.log(files);

  const uploadFile = async () => {
    // 이미지 용량 최적화 과제
    const file = files[0];
    const name = file.name;
    const imgRef = refImage(storage, name);
    const res = await uploadBytes(imgRef, file);
    // url을 클릭하면 실제 이미지를 볼 수 있음
    const url = await getDownloadURL(imgRef);

    return url;
  };
  async function writeUserData(imgUrl) {
    // set으로 하면 기존에 있던 목록의 이름과 겹치면 그것이 업데이트 되기 때문에 push사용
    await push(ref(db, "items/"), {
      title,
      price,
      description,
      place,
      insertAt: new Date().getTime(),
      imgUrl,
    });

    window.location.hash = "/";
  }

  const handleSubmit = async () => {
    const imgUrl = await uploadFile();
    writeUserData(imgUrl);
  };
</script>

<form id="write-form" on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="image">이미지</label>
    <input type="file" bind:files id="image" name="image" />
  </div>
  <div>
    <label for="title">제목</label>
    <input type="text" id="title" name="title" bind:value={title} />
  </div>
  <div>
    <label for="price">가격</label>
    <input type="number" id="price" name="price" bind:value={price} />
  </div>
  <div>
    <label for="description">설명</label>
    <input
      type="text"
      id="description"
      name="description"
      bind:value={description}
    />
  </div>
  <div>
    <label for="place">장소</label>
    <input type="text" id="place" name="place" bind:value={place} />
  </div>
  <div>
    <button class="write-button" type="submit">글쓰기완료</button>
  </div>
</form>

<Footer location="write" />

<style>
  .write-button {
    background-color: tomato;
    margin: 10px;
    border-radius: 10px;
    padding: 5px 12px 5px 12px;
    color: white;
    cursor: pointer;
  }
</style>
