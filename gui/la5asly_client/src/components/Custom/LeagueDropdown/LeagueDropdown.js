import React, { Component } from "react";
import { Dropdown, Image } from "react-bootstrap";
import { connect } from "react-redux";
import "./LeagueDropdown.css";

const CustomMenu = React.forwardRef(
  ({ children, style, className, "aria-labelledby": labeledBy }, ref) => {
    return (
      <div
        ref={ref}
        style={style}
        className={className}
        aria-labelledby={labeledBy}
      >
        <ul className="list-unstyled">{React.Children.toArray(children)}</ul>
      </div>
    );
  }
);

const CustomToggle = React.forwardRef(({ children, onClick }, ref) => (
  <a
    href=""
    ref={ref}
    onClick={(e) => {
      e.preventDefault();
      onClick(e);
    }}
  >
    {children}
    &#x25bc;
  </a>
));

class LeagueDropdown extends Component {
  render() {
    return (
      <Dropdown>
        <Dropdown.Toggle as={CustomToggle} id="dropdown-custom-components">
          Custom toggle
        </Dropdown.Toggle>

        <Dropdown.Menu as={CustomMenu}>
          {this.props.leagues &&
            this.props.leagues.map((league) => {
              return (
                <Dropdown.Item eventKey={league.name}>
                  <Image className="league-logo" src={league.logo} />{" "}
                  {league.name}
                </Dropdown.Item>
              );
            })}
        </Dropdown.Menu>
      </Dropdown>
    );
  }
}
const mapStateToProps = (store) => {
  return { leagues: store.teams.leagues };
};

export default connect(mapStateToProps, {})(LeagueDropdown);
