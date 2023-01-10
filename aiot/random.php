<?php

$light = $GET["light"];
$humi = $GET["humi"];
$temp = $GET["temp"];

// Create connection
$mysqli = new mysqli("localhost", "test123", "test123", "aiotdb");

// Check connection
if ($mysqli->connect_error) {
  echo ("Connection failed: " . $mysqli->connect_error);
  exit();
}
//讓AI把資料分類完後回到random好比較
$SQL="UPDATE sensors SET status=rand() where true";

if ($result = $mysqli->query("$SQL"))
    ;

    $mysqli->close();

    header("Location: http://localhost/aiot/");
        ?>


