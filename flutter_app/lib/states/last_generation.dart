import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LastGeneration extends ChangeNotifier {
  late SharedPreferences _prefs;

  LastGeneration() {
    initialize();
  }

  Future<void> initialize() async {
    _prefs = await SharedPreferences.getInstance();
    _previousOperation = _prefs.getString('_previousOperation') ?? '';
    notifyListeners();
  }

  String _previousOperation = '';
  String get getPreviousOperation => _previousOperation;
  Future<void> setPreviousOperation(String value) async {
    _previousOperation = value;
    await _prefs.setString('_previousOperation', value);
    notifyListeners();
  }

}
