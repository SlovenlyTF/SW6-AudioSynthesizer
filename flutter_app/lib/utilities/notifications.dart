import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';

void showDebugToast(String message, [Color? color]) {
  Fluttertoast.showToast(
      msg: message,
      toastLength: Toast.LENGTH_LONG,
      gravity: ToastGravity.CENTER,
      timeInSecForIosWeb: 1,
      backgroundColor: color ?? Colors.blue,
      textColor: Colors.white,
      fontSize: 16.0);
}