import React, {Component} from 'react';

class NotFound extends Component {
    render() {
        return (
            <div style={{
                position: "absolute",
                height: "200px",
                zIndex: "15",
                top: "50%",
                left: "50%",
                margin: "-100px 0 0 -150px",
            }}>
                <h1>PAGE NOT FOUND</h1>
            </div>
        );
    }
}

export default NotFound;