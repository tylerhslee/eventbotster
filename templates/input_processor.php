<?php
$userIn = $_POST["userIn"];

//Compose CSV String
$userStr = $userIn . ",";

$db = fopen( "queryDB.txt", "a" );
fputs( $db, $userStr );
fclose( $db );

header('Location: http://process.austinserio.com/index.html');

?>