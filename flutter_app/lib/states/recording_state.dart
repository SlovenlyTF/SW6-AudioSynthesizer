import 'package:flutter/material.dart';
import 'package:flutter_app/utilities/file_system.dart';
import 'package:flutter_app/utilities/notifications.dart';
import 'package:record/record.dart';
import 'package:shared_preferences/shared_preferences.dart';

class RecordingState extends ChangeNotifier {
  late SharedPreferences _prefs;

  RecordingState() {
    initialize();
  }

    // Using a bool for now, perhaps refactor to an enum in the future
  bool _isRecording = false;
  bool get getIsRecording => _isRecording;
  bool _recordingExists = false;
  bool get getRecordingExists => _recordingExists;
  bool _newRecording = false;
  bool get getNewRecording => _newRecording;

  Future<void> initialize() async {
    _prefs = await SharedPreferences.getInstance();
    _recordingExists = _prefs.getBool('_recordingExists') ?? false;
    _newRecording = _prefs.getBool('_newRecording') ?? false;
    notifyListeners();
  }

  // TODO: Was a global variable, now it's here, fucking dumb x2
  final record = AudioRecorder();

  Future<void> setIsRecording(bool value) async {
    _isRecording = value;
    await _prefs.setBool('_isRecording', value);
    notifyListeners();
  }

  void setRecordingExists(bool value) async {
    _recordingExists = value;
    await _prefs.setBool('_recordingExists', value);
    notifyListeners();
  }

  void setNewRecording(bool value) async {
    _newRecording = value;
    await _prefs.setBool('_newRecording', value);
    notifyListeners();
  }

  void startRecording() async {
    // TODO: Properly request permission if not given
    if (!await record.hasPermission()) {
      showDebugToast("Please grant permission to record audio", Colors.red);
      return;
    }
    // Start recording to file
    setIsRecording(true);
    String filePath = await getTempRecordingPath();
    
    await record.start(
      const RecordConfig(encoder: AudioEncoder.wav),
      path: filePath,
    );
    // showDebugToast("Recording started");
  }

  void stopRecording() async {
    await record.stop();
    setIsRecording(false);
    setRecordingExists(true);
    setNewRecording(true);
    // showDebugToast("Recording stopped");
  }

  void deleteRecording() async {
    record.dispose();
  }
}
