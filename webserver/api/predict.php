<?php
  // include 'config.php';

  $postdata = file_get_contents("php://input");
  $requestList = json_decode($postdata, true);


  foreach($requestList as $req){
    //PHP will call python each pair one by one
    //Python will return string in format=com_id|pro_id|weight|source|time_stamp

    $command = escapeshellcmd("python /home/ajmalkurnia/Dataset_skripsi/predict.py "
              .$req['comId']." ".$req['proId']);
    $output = shell_exec($command);
    $output = explode("|",$output);

    $source = $output[3];
    $weight = trim($output[2]);
    $timestamp = $output[4];
    $row = array('com_id'=>$output[0],'pro_id'=>$output[1],
                 'weight'=>$weight,'source'=>$source,'timestamp'=>$timestamp);
    $respArr[] = $row;
  }
  header('Content-type: application/json');
  echo json_encode($respArr);
?>