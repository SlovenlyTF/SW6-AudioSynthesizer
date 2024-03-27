import 'package:flutter/material.dart';
import 'package:flutter_app/utilities/file_system.dart';
import 'package:flutter_app/utilities/notifications.dart';
import 'package:record/record.dart';

class RecordingState extends ChangeNotifier {
  // Using a bool for now, perhaps refactor to an enum in the future
  bool _isRecording = false;

  bool get getIsRecording => _isRecording;

  // TODO: Was a global variable, now it's here, fucking dumb x2
  final record = AudioRecorder();

  void setIsRecording(bool value) {
    _isRecording = value;
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
    // showDebugToast("Recording stopped");
  }

  void deleteRecording() async {
    record.dispose();
  }
}
