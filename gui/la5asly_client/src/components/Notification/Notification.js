import React from 'react';
import {connect} from 'react-redux';
import "./Notification.css"

class NotificationBox extends React.Component {
    render() {
        let notifyClass = "notification";
        if (this.props.notify.display) {
            notifyClass += " show";
        }
        return (
            <div className={`${notifyClass} lead`}>
                {this.props.notify.message}
            </div>
        )
    }
}

export default connect(
    state => ({notify: state.notifications})
)(NotificationBox);