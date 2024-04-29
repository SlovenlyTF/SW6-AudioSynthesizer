import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_app/states/generation_option_state.dart';
import 'package:flutter_app/states/last_generation.dart';
import 'package:flutter_app/states/recording_state.dart';
import 'package:flutter_app/utilities/file_system.dart';
import 'package:flutter_app/utilities/notifications.dart';
import 'package:flutter_app/states/audio_saved_state.dart';

const SERVER_IP = String.fromEnvironment('SERVER_IP', defaultValue: '10.0.2.2:5000');

class GenerationState extends ChangeNotifier {

  GenerationState() {
    getTempGeneratedPath().then((path) {
      setFileExists(File(path).existsSync());
    });
  }

  // Using a bool for now, perhaps refactor to an enum in the future
  bool _isGenerating = false;
  bool get getGenerating => _isGenerating;
  void setGenerating(bool value) {
    _isGenerating = value;
    notifyListeners();
  }

  // To future employers, this is not indicative of my programming skills, I swear
  bool _haveReloadedAudioplayer = false;
  bool get getHaveReloadedAudioplayer => _haveReloadedAudioplayer;
  void setHaveReloadedAudioplayer(bool value) {
    _haveReloadedAudioplayer = value;
  }

  bool _fileExists = false;
  bool get getFileExists => _fileExists;
  void setFileExists(bool value) {
    _fileExists = value;
    notifyListeners();
  }

  bool _audioHasGenerated = false;
  bool get getAudioHasGenerated => _audioHasGenerated;
  void setAudioHasGenerated(bool value) {
    _audioHasGenerated = value;
    notifyListeners();
  }

  // TODO: Split function
  void generateAudio(GenerationOptionState generationOptions, AudioSavedState audioSavedState, 
                      GenerationOptionState generationOptionState, RecordingState recordingState,
                      LastGeneration lastGeneration) async {
    try {
      setGenerating(true);
      // showDebugToast('Sending audio to server');

      String resultUri = await sendRecording(generationOptions.getOperation);

      if(resultUri.isEmpty) {
        showDebugToast('Failed to receive response from server', Colors.red);
      } else {
        // showDebugToast('Received response from server, downloading audio');

        try {
          // TODO: Verify received URI before downloading
          bool downloadSuccessful = await downloadRecording(resultUri);
          if(downloadSuccessful) {
            // showDebugToast('Audio successfully downloaded!');
          } else {
            showDebugToast('Failed to download audio from server', Colors.red);
          }
        } catch (error) {
          showDebugToast('Failed to download audio from server', Colors.red);
        }
      }
    } finally {
      setGenerating(false);
      setHaveReloadedAudioplayer(false);
      audioSavedState.setIsAudioSaved(false);
      lastGeneration.setPreviousOperation(generationOptionState.getOperation.label);
      recordingState.setNewRecording(false);
    }
  }

  Future<String> sendRecording(OperationLabel operation) async {
    // Define paths
    var url = Uri.http(SERVER_IP, 'api/${operation.endpoint}');
    String filePath = await getTempRecordingPath();

    // Prepare request
    Dio dio = Dio();
    dio.options.headers['Connection'] = 'Keep-Alive';
    dio.options.contentType = 'multipart/form-data';
    dio.options.connectTimeout = const Duration(seconds: 20);
    FormData formData = FormData.fromMap({
      'audio': await MultipartFile.fromFile(filePath, filename: 'test.wav'),
      ...operation.parameters ?? {},
    });

    print("ENDPOINT:");
    print(url.toString());

    print("PARAMTERS:");
    print({
      'audio': await MultipartFile.fromFile(filePath, filename: 'test.wav'),
      ...operation.parameters ?? {},
    });

    // Send request
    Response response;
    try {
      response = await dio.post(url.toString(), data: formData);
    } catch (error) {
      print('Error: $error');
      return '';
    }

    // TODO: Handle jsend style status and error messages when talking with server
    if (response.statusCode != 200) {
      print('Sound synthesis failed with status: ${response.statusCode}');
      return '';
    }

    return response.data['data']['resultUrl'];
  }

  Future<bool> downloadRecording(String url) async {
    String filePath = await getTempGeneratedPath();

    // Prepare request
    Dio dio = Dio();
    dio.options.headers['Connection'] = 'Keep-Alive';
    dio.options.connectTimeout = const Duration(seconds: 30);

    // Send request
    try {
      var response = await dio.download(url, filePath);
      var isSuccessful = response.statusCode == 200;
      if(isSuccessful) {
        setFileExists(true);
      }
      return isSuccessful;
    } catch (error) {
      print('Error: $error');
      return false;
    }
  }
}
