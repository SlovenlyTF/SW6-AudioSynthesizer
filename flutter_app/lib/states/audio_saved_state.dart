import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AudioSavedState extends ChangeNotifier {
  late SharedPreferences _prefs;

  AudioSavedState() {
    initialize();
  }

  bool _isAudioSaved = false;
  bool get getIsAudioSaved => _isAudioSaved;

  Future<void> initialize() async {
    _prefs = await SharedPreferences.getInstance();
    _isAudioSaved = _prefs.getBool('_isAudioSaved') ?? false;
    notifyListeners();
  }

  Future<void> setIsAudioSaved(bool value) async {
    _isAudioSaved = value;
    await _prefs.setBool('_isAudioSaved', value);
    notifyListeners();
  }
}
