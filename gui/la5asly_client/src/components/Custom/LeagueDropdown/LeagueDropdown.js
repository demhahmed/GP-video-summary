import React, { Component } from "react";
import { Dropdown, Image } from "react-bootstrap";
import { connect } from "react-redux";
import "./LeagueDropdown.css";
import { FaCaretDown, FaCaretUp } from "react-icons/fa";

class LeagueDropdown extends Component {
  state = {
    down: true,
    leagueName: null,
    logo: null,
  };
  CustomMenu = React.forwardRef(
    ({ children, style, className, "aria-labelledby": labeledBy }, ref) => {
      return (
        <div
          ref={ref}
          style={style}
          className={className + " darkmode"}
          aria-labelledby={labeledBy}
        >
          <ul className="list-unstyled">{React.Children.toArray(children)}</ul>
        </div>
      );
    }
  );

  CustomToggle = React.forwardRef(({ children, onClick }, ref) => (
    <div>
      <button
        ref={ref}
        className="my-filter-btn"
        onClick={(e) => {
          e.preventDefault();
          // this.setState({ down: !this.state.down });
          onClick(e);
        }}
      >
        {children}
      </button>
      {this.state.down ? (
        <FaCaretDown
          onClick={(e) => {
            e.preventDefault();
            onClick(e);
          }}
          className="caret-dropdown"
        />
      ) : (
        <FaCaretUp
          onClick={(e) => {
            e.preventDefault();
            onClick(e);
          }}
          className="caret-dropdown"
        />
      )}
    </div>
  ));
  render() {
    return (
      <Dropdown className={this.props.className}>
        <Dropdown.Toggle as={this.CustomToggle} id="dropdown-custom-components">
          {this.state.leagueName ? (
            <div>
              <Image className="league-logo" src={this.state.logo} />
              {this.state.leagueName}
            </div>
          ) : (
            "Select League"
          )}
        </Dropdown.Toggle>

        <Dropdown.Menu className="right-dropdown" as={this.CustomMenu}>
          {this.props.leagues &&
            this.props.leagues.map((league) => {
              return (
                <Dropdown.Item
                  onClick={() => {
                    if (this.props.onChange) this.props.onChange(league._id);
                    this.setState({
                      leagueName: league.name,
                      logo: league.logo,
                    });
                    if (this.props.handleLeagueSelect) {
                      this.props.handleLeagueSelect(league._id);
                    }
                  }}
                  eventKey={league.name}
                >
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
