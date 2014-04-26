#!/usr/bin/lua
local JSON = dofile("contrib/JSON.lua")
local http = require "socket.http"

local map_response, map_code = http.request("http://aqicn.org/map/world/")
local parsed_table = JSON:decode(string.gsub(map_response, "^.-mapInitWithData%((.-)%);.*$", "%1"))

for k,v in pairs(parsed_table) do
	print(v.city .. "\t" .. v.aqi .. "\t" .. v.g[1] .. " " .. v.g[2] .. "\t" .. v.utime)
end

