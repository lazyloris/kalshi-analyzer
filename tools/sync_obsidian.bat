@echo off
REM Pull the latest bot results from GitHub and copy them into Obsidian.
REM Schedule this daily with Windows Task Scheduler if you like.
cd /d "%~dp0.."
python tools\sync_obsidian.py "D:\Obsidian_Vaults\Projects\Kalshi Trader"
