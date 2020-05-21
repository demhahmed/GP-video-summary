const fs = require("fs");
const express = require("express");
const mongoose = require("mongoose");
const downloadFile = require("../utils/download");

const Team = require("../models/Team");
const League = require("../models/League");

const router = new express.Router();

/**
 * This route fetch all leagues
 */
router.get("/api/fetch_leagues", async (req, res) => {
  try {
    const data = await League.find();
    res.status(200).send(data);
  } catch (error) {
    res.status(404).send({ error: error.message });
  }
});

/**
 * This route a league teams.
 */
router.get("/api/fetch_league_teams", async (req, res) => {
  try {
    let teams = await Team.find({}).populate("league");
    const leagueType = req.query.leagueType;
    if (leagueType) {
      teams = teams.filter((team) => team.league.name === leagueType);
    }
    res.status(200).send(teams);
  } catch (error) {
    console.log(error);
    res.status(404).send({ error: error.message });
  }
});

/**
 * This route used to load local data to database
 */
router.post("/api/generate_data", async (req, res) => {
  try {
    const data = JSON.parse(fs.readFileSync("data/team-logos.json"));
    const leagues = {};
    for (league of data) {
      const savedLeague = await new League({
        name: league.leagueType,
        logo: league.logo,
      }).save();
      leagues[savedLeague.name] = savedLeague;
    }
    for (league of data) {
      for (team of league.teams) {
        await new Team({
          name: team.teamName,
          logo: team.logo,
          league: leagues[league.leagueType]._id,
        }).save();
      }
    }
    res.send();
  } catch (error) {
    console.log(error);
    res.status(404).send({ error: error.message });
  }
});

/**
 * This route get the logos from another place to be hosted in our server.
 */
router.post("/api/host_logos", async (req, res) => {
  try {
    const data = JSON.parse(fs.readFileSync("data/team-logos.json"));
    const leagues = {};
    for ({ teams, leagueType, logo } of data) {
      const leg_path = leagueType.replace(" ", "_").toLowerCase() + "_.png";
      const folder = "/logos/leagues";
      await downloadFile(logo, folder, leg_path);
      const savedLeague = await new League({
        name: leagueType,
        logo: "/logos/leagues" + leg_path,
      }).save();
      leagues[leagueType] = savedLeague._id;
    }
    for ({ teams, leagueType, leg_logo } of data) {
      for ({ logo: team_logo, teamName } of teams) {
        const folder = "/logos/teams";
        const file_name =
          leagueType.replace(" ", "_").toLowerCase() +
          "_" +
          teamName.replace(" ", "_").toLowerCase() +
          "_logo.png";
        await downloadFile(team_logo, folder, file_name);
        await new Team({
          name: teamName,
          logo: file_name,
          league: leagues[leagueType],
        }).save();
      }
    }
    res.status(200).send();
  } catch (error) {
    res.status(400).send(error.message);
  }
});



module.exports = router;
