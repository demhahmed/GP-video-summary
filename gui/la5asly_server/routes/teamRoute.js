const fs = require("fs");
const express = require("express");

const mongoose = require("mongoose");

const Team = mongoose.model("Team");
const League = mongoose.model("League");

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

module.exports = router;
