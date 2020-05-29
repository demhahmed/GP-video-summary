import React, { Component } from "react";
import { Dropdown, Image } from "react-bootstrap";
import { FaCaretUp, FaCaretDown } from "react-icons/fa";
import { connect } from "react-redux";
import _ from 'lodash';
class TeamsDropdown extends Component {
  state = {
    down: true,
    teamName: null,
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
    let sortedTeams = this.props.teams.filter(
      (team) => team.league._id === this.props.leagueId
    );
    sortedTeams = _.sortBy(sortedTeams, 'name')
    return (
      <Dropdown className={this.props.className}>
        <Dropdown.Toggle as={this.CustomToggle} id="dropdown-custom-components">
          {this.state.teamName ? (
            <div>
              <Image className="league-logo" src={this.state.logo} />
              {this.state.teamName}
            </div>
          ) : (
            "Select Team"
          )}
        </Dropdown.Toggle>

        <Dropdown.Menu
          className="right-dropdown"
          style={{ maxHeight: "200px", overflow: "auto" }}
          as={this.CustomMenu}
        >
          {sortedTeams &&
            sortedTeams.map((team) => {
              return (
                <Dropdown.Item
                  onClick={() => {
                    this.setState({
                      teamName: team.name,
                      logo: team.logo,
                    });
                    if (this.props.handleTeamSelect) {
                      this.props.handleTeamSelect(team._id);
                    }
                  }}
                  eventKey={team.name}
                >
                  <Image className="league-logo" src={team.logo} /> {team.name}
                </Dropdown.Item>
              );
            })}
        </Dropdown.Menu>
      </Dropdown>
    );
  }
}
const mapStateToProps = (store) => {
  return { teams: store.teams.teams };
};

export default connect(mapStateToProps, {})(TeamsDropdown);
