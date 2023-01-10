<?php
$light = 0;
$humi = 0;
$temp = 0;

if(!empty($_GET['light'])) {
    $light = $_GET['light'];
}
if(!empty($_GET['humi'])) {
    $humi = $_GET['humi'];
}
if(!empty($_GET['temp'])) {
    $temp = $_GET['temp'];
}

$light = $_GET['light'];
$humi = $_GET['humi'];
$temp = $_GET['temp'];

// Create connection
$mysqli = new mysqli("localhost", "test123", "test123", "aiotdb");

// Check connection
if ($mysqli->connect_error) {
  echo ("Connection failed: " . $mysqli->connect_error);
  exit();
}

$sqlquery = "insert into sensors (light, humi, temp) VALUES ($light, $humi, $temp)";
$result = $mysqli->query($sqlquery);

$mysqli->close();

header("Location: http://localhost/aiot/");
    ?>