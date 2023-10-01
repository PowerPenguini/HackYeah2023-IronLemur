<script>
  import locationSvg from "../src/assets/location.svg";
  import sendSvg from "../src/assets/send.svg";
  import logoSvg from "../src/assets/logo.svg";
  import axios, { formToJSON } from "axios";
  import Loader from "./lib/Loader.svelte";

  let textarea;
  let nothing;
  let history = {};
  let recommendations = [];
  let isLoading = false;
  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); // Zapobieganie przejściu do nowej linii w textarea
      submitMsg(event); // Wywołanie handleSubmit po naciśnięciu Enter
    }
  }
  const submitMsg = async (event) => {
    event.preventDefault(); 
    isLoading = true
    if (textarea.value.trim() == "")
    {
      isLoading = false
      return;
    }
    let cachedMessage = textarea.value;
    textarea.value = "";
  

    try {
      const response = await axios.post("http://localhost:8000/ai-msg", {message: cachedMessage});
      const data = response.data;
      console.log(data.recommendations);
      history[cachedMessage] = data.text;
      recommendations = data.recommendations;
      if (recommendations.length > 0) {
        nothing.classList.add("hidden");
      } else {
        nothing.classList.remove("hidden")
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
    isLoading = false;

  };
</script>
<nav><img src="{logoSvg}" alt=""></nav>
<main>
  <section class="recommended">
    <h1>Rekomendacje</h1>
    <div class="recommended-wrapper">
      <div class="nth" bind:this="{nothing}">Porozmawiaj ze AI aby otrzymać rekomendacje</div>
      {#if recommendations}
      {#each recommendations as r}
      <div class="recommended-card">
        <h2>{r.name}</h2>
        <div class="location"><img src="{locationSvg}" alt="">{r.city}</div>
        <p>{r.description}</p>
        <div class="tag-cloud">
          {#each r.tags as tag}
            <div class="tag">{tag}</div>
          {/each}
        </div>
      </div>
      {/each}
      {/if}
    </div>
  </section>
  <section class="chat">
    <h1>AI-Doradca</h1>
    <div class="chat-wrapper">
      <div class="chat-pair">
        <div class="bot"><div>Hej! Jestem Agama, mogę pomóc Ci wybrać ścieżkę kariery, kierunek studiów lub odpowiedzieć na pytania związane ze studiami.</div></div>
      </div>
      {#each Object.entries(history) as [human, bot]}
      <div class="chat-pair">
        <div class="human"><div>{human}</div></div>
        <div class="bot"><div>{bot}</div></div>
      </div>
      {/each}
      <Loader {isLoading}/>
    </div>
    <form on:submit|preventDefault={submitMsg} class="prompt-enter">
      <textarea class="textarea" placeholder="Jakie masz hobby? Co chciałbyś studiować?" bind:this={textarea} on:keydown={handleKeyPress}></textarea>
      <button class="button" on:click={submitMsg}><img src="{sendSvg}" alt=""></button>
    </form>
  
  </section>
</main>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');
  ::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background-color: #f1f1f1; /* Light background color */
}

::-webkit-scrollbar-thumb {
  background-color: #888; /* Color of the scrollbar thumb */
  border-radius: 5px; /* Rounded corners for the thumb */
}

::-webkit-scrollbar-thumb:hover {
  background-color: #555; /* Color of the thumb on hover */
}


/* Edge and IE scrollbar */
/* Note: Edge and IE use the old-style scrollbar customization */
/* You can use these rules to style the scrollbar for these browsers. */
/* Keep in mind that these browsers are becoming less common. */
/* The first color is the thumb color, and the second is the track color. */
/* In this example, it's set to a light style. */
/* Replace these colors as needed. */
body {
  scrollbar-face-color: #888;
  scrollbar-track-color: #f1f1f1;
}
main {
  display: flex;
}
section {
  width: 50vw;
  height: 100vh;
  padding: 50px;
  border: solid 1px #eee;
}
.tag-cloud {
  display: flex;
  border-radius: 20px;
  gap: 10px
}
.tag {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 20px;
  background-color: #D28B0055;
}
.location {
  display: flex;
  gap: 10px;
  font-weight: 600;
}
.recommended-card {
  padding: 10px 
  border-box
}
.recommended-wrapper {
  display: flex;
  flex-direction: column;
  gap: 30px;
  height: 75vh;
  overflow-y: auto;
  padding-right: 10px;
}
.textarea {
  width: calc(100% - 50px);
  resize: none;
  border-radius: 20px;
  padding: 14px;
  font-family: Ubuntu, sans-serif;
  font-size: 16px;
  border-radius: 10px 0 0 10px;
  display: block;
  border: solid 1px #ccc;
}
.prompt-enter {
  display: flex;
}
.button {
  background-color: #D28B00bb;
  display: grid;
  place-items: center;
  border-radius: 0 10px 10px 0;
  width: 50px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.button:hover {
  background-color: hsl(40, 100%, 70%);
}
.button img {
  fill: #213547;
}
.chat-wrapper {
  width: 100%;
  height: calc(100% - 200px);
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
  margin-bottom: 20px;
}
.chat-pair {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
}
.human {
  grid-row: 1/2;
  padding: 10px;
  grid-column: 2/3;
}
.bot {
  grid-row: 2/3;
  grid-column: 1/2;
}
.bot div {
  background-color: #eee;
  padding: 10px;
  border-radius: 4px 20px 20px 20px;

}
.human div {
  background-color: #D28B00ee;
  padding: 10px;
  border-radius: 20px 4px 20px 20px;
}
.nth {
  padding-top: 45%;
  font-size: 25px;
  color: #ccc
}
:global(.hidden) { 
  display: none;
}
nav {
  position: fixed;
  top: 0;
  left: 0;
  padding: 30px;
}
nav img {
  width: 120px;
}
</style>