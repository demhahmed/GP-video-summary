import React from "react";
import "./TooltipError.css";

import {FaCaretLeft} from "react-icons/fa";

export default function TooltipError(props) {
  return (
    <div className={props.className + " my-tooltip"}>
      <FaCaretLeft className="caret" />
      <p>{props.error_msg}</p>
    </div>
  );
}
