import React from "react";
import SendIcon from "@mui/icons-material/Send";

const Chat = () => {
  return (
    <section>
      <div></div>
      <div className="form-container">
        <form className="form">
          <input
            type="text"
            placeholder="Zadaj pytanie"
            className="input"
          ></input>
          <button className="btn">
            <SendIcon className="send-icon" />
          </button>
        </form>
      </div>
    </section>
  );
};

export default Chat;
