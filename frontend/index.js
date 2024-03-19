const calcTime = (timeStamp) => {
  // 한국시간 UTC + 9
  const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
  const passedTime = new Date(curTime - timeStamp);
  const hours = passedTime.getHours();
  const minutes = passedTime.getMinutes();
  const seconds = passedTime.getSeconds();

  if (hours > 0) return ` ${hours}시간 전`;
  else if (minutes > 0) return ` ${minutes}분 전`;
  else if (seconds > 0) return ` ${seconds}초 전`;
  else return "방금 전";
};

const renderData = (data) => {
  // data 형식
  // data = [{id:1, title:'aaaa'}, {id:2, title:'afasfasf'}]
  // 서버측에서는 가장 나중에 온데이터가 최근 데이터므로 최근데이터 부터 표현하기
  // 위해 배열.reverse사용(순서를 역으로 바꿈 )

  const main = document.querySelector("main");
  data.reverse().forEach(async (obj) => {
    const div = document.createElement("div");
    div.className = "items-list";

    const imgDiv = document.createElement("div");
    imgDiv.className = "items-list__img";
    //img add
    const img = document.createElement("img");
    const res = await fetch(`/images/${obj.id}`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    img.src = url;

    const InfoDiv = document.createElement("div");
    InfoDiv.className = "items-list__info";

    const InfoTitleDiv = document.createElement("div");
    InfoTitleDiv.className = "items-list__info-title";
    InfoTitleDiv.innerText = obj.title;

    const InfoMetaDiv = document.createElement("div");
    InfoMetaDiv.className = "items-list__info-meta";
    InfoMetaDiv.innerText = obj.place + calcTime(obj.insertAt);

    const InfoPriceDiv = document.createElement("div");
    InfoPriceDiv.className = "items-list__info-price";
    InfoPriceDiv.innerText = obj.price;

    imgDiv.appendChild(img);

    InfoDiv.appendChild(InfoTitleDiv);
    InfoDiv.appendChild(InfoMetaDiv);
    InfoDiv.appendChild(InfoPriceDiv);
    div.appendChild(imgDiv);
    div.appendChild(InfoDiv);
    main.appendChild(div);
  });
};

const fetchList = async () => {
  const res = await fetch("/items");
  const data = await res.json();
  renderData(data);
};

fetchList();
