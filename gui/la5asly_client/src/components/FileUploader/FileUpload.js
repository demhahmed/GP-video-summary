import React, { Fragment, useState } from "react";
import Progress from "./Progress";

class FileUpload extends React.Component {
  state = {
    filename: "Choose File",
    file: null,
  };
  onChange = (e) => {
    if (!e.target.files || (e.target.files && e.target.files.length === 0))
      return;
    if (this.props.onImageSelected) {
      this.props.onImageSelected(e.target.files[0]);
    }
    this.setState({
      file: e.target.files[0],
      filename: e.target.files[0].name,
    });
  };
  render() {
    return (
      <div className="custom-file mb-4">
        <input
          type="file"
          className="custom-file-input"
          id="customFile"
          onChange={this.onChange}
        />
        <label
          style={this.props.style}
          className="custom-file-label"
          htmlFor="customFile"
        >
          {this.state.filename}
        </label>
      </div>
    );
  }
}

export default FileUpload;
