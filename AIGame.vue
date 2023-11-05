<template>
  <div class="aigame">
    <Header />
    <div class="gameCard">
      <img v-show="!imgLoaded" id="placeholdImg" :src="loadingImage" alt="" />
      <img v-show="imgLoaded" :src="imgList[imgIndex]" alt="" />
      <div class="bottomContent">
        <h3>NPC : {{ npcAnswer }}</h3>
        <ul>
          <li
            @click="choose(index, content)"
            v-for="(content, index) in answerList"
            :key="index"
            :class="{ active: isActive }"
          >
            {{ `${index + 1}.${content}` }}
          </li>
        </ul>
        <div class="inputContainer" v-show="showAskNPC">
          Ask NPC:
          <input
            v-model="inputContent"
            @keyup.enter="handleInputEnter"
          /><button @click="handleInputEnter">确定</button>
        </div>
      </div>
      <div v-if="loading" class="mask" :class="{ contentLoading: loading }">
        <img src="../assets/images/loadingCircle.webp" alt="" />
      </div>
    </div>
  </div>
</template>

<script>
import Header from "../components/header.vue";
import debounce from "lodash/debounce";
export default {
  components: { Header },
  data() {
    return {
      showVideoOrImg: true,
      imgIndex: 0,
      videoIndex: 0,
      imgLoaded: false,
      videoLoaded: false,
      onlyCanClickOnceFlag: false,
      url: window.urls,
      imgList: [
        require("../assets/images/aigame1.webp"),
        require("../assets/images/aigame2.webp"),
        require("../assets/images/aigame3.webp"),
        require("../assets/images/aigame4.webp"),
      ],
      videoList: [require("../assets/images/aigamevideo1.mp4")],
      initialState: {},
      npcAnswer: "你是谁？那伫立在门口不肯进入的孩童？",
      answerList: [
        "我只是个过客。抱歉打扰。",
        "我……我是个学生，我想成为一名艺术家。",
        "我是一位计算机工程师。",
      ],
      tempAnswer: "",
      tempAnswerList: [],
      loadingImage: require("../assets/images/loading.webp"),
      showAskNPC: true,
      inputContent: "",
      isActive: false,
      loading: false,
    };
  },
  created() {
    this.tempAnswer = this.npcAnswer;
    this.tempAnswerList = this.answerList;
    this.handleInputEnter = debounce(this.handleInputEnter, 300);
  },
  methods: {
    handleInputEnter() {
      if (!this.fullscreenLoading) {
        // 内部进行操作
        this.loading = true;

        this.$axios
          .post(this.url + "baiduapi_ask", {
            question: this.inputContent,
          })
          .then((res) => {
            console.log("res:", res);
            this.npcAnswer = res.data.result;
            this.answerList = ["返回"];
            this.loading = false;
          });
      }
    },
    /**
     *
     * @param {*} option 选择是哪一个选项
     */
    choose(option, content) {
      console.log("content:", content);
      if (content == "返回") {
        this.onlyCanClickOnceFlag = false;
        this.imgIndex = 0;
        this.answerList = this.tempAnswerList;
        this.npcAnswer = this.tempAnswer;
        this.showAskNPC = true;
        return;
      }
      if (!this.onlyCanClickOnceFlag) {
        this.showAskNPC = false;
        switch (option) {
          case 0:
            this.answerList = [
              "你合上了这扇门，爱、激情和创造、痛苦的门。",
              "返回",
            ];
            this.imgIndex = 1;
            break;
          case 1:
            this.answerList = ["进来吧，人类之子。", "返回"];
            this.imgIndex = 2;
            break;
          case 2:
            this.answerList = [
              "你好，我是活在数据世界的达利。跑在历史前面比描绘它更有趣。请进。",
              "返回",
            ];
            this.imgIndex = 3;
            break;
          default:
            break;
        }
        this.onlyCanClickOnceFlag = true;
      }
    },
    /**
     *
     * @param {*} type
     * @param {*} list
     * 处理一下图片列表和视频列表的函数，确保完全加载再显示
     */
    processAssets(type, list) {
      console.log("type:", type);
      console.log("list:", list);
      const promises = list.map((assetSrc) => {
        console.log("assetSrc:", assetSrc);
        return new Promise((resolve, reject) => {
          if (type == "img") {
            console.log("处理图片:");
            const img = new Image();
            img.onload = () => {
              resolve(img);
            };
            img.onerror = (err) => {
              reject(err);
            };
            img.src = assetSrc;
          } else {
            console.log("处理视频:");
            const video = document.createElement("video");
            video.onloadeddata = () => {
              resolve(video);
            };
            video.onerror = (err) => {
              reject(err);
            };
            video.src = assetSrc;
          }
        });
      });
      Promise.all(promises)
        .then(() => {
          console.log("这里了？:");
          type == "img" ? (this.imgLoaded = true) : (this.videoLoaded = true);
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  mounted() {
    this.processAssets("video", this.videoList);
    this.processAssets("img", this.imgList);
  },
};
</script>

<style scoped lang="less">
.aigame {
  background-color: #ebebeb;
  color: #fff;
  width: 100%;
  height: 100%;
  user-select: none;
  & .gameCard {
    margin: 0 auto;
    width: 30%;
    min-width: 500px;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    margin-top: 10vh;
    position: relative;

    @media screen and (max-width: 600px) {
      width: 90%;
      height: 500px;
      min-width: 0;
      font-size: 12px;
      & h3 {
        font-size: 14px;
      }
    }

    & img,
    video {
      width: 100%;
      height: 100%;
      border-radius: 20px;
      object-fit: cover;
    }

    & .bottomContent {
      width: 96%;
      background-color: rgba(0, 0, 0, 0.9);
      padding: 15px;
      box-sizing: border-box;
      border-radius: 20px;
      position: absolute;
      left: 2%;
      bottom: 2%;
      z-index: 1;
      @media screen and (max-width: 600px) {
        padding: 10px;
      }
      & ul {
        width: fit-content;

        & li {
          cursor: pointer;
          padding: 5px 0;

          &:hover {
            color: orange;
          }
        }
        & li.active {
          color: orange;
        }
      }
    }
    & .mask {
      display: flex;
      align-content: center;
      justify-content: center;
      flex-wrap: wrap;
      @keyframes rotate {
        0% {
          transform: rotate(0);
        }
        100% {
          transform: rotate(360deg);
        }
      }
      & img {
        width: 64px;
        height: 64px;
        animation: rotate 1.5s linear infinite forwards;
      }
    }
    & .mask.contentLoading {
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.6);
      position: absolute;
      left: 0;
      bottom: 0;
      z-index: 99;
      border-radius: 20px;
    }
    & .inputContainer {
      position: relative;

      width: max-content;
      & input {
        width: max-content;
        border: none;
        outline: none;
        border-radius: 4px;
        padding: 5px;
        padding-right: 35px;
      }
      & button {
        position: absolute;
        right: 2px;
        top: 50%;
        transform: translateY(-50%);
      }
    }
  }
}
</style>