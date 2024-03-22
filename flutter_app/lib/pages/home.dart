import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:fluttertoast/fluttertoast.dart';

import 'package:flutter_app/widgets/audio_controller.dart';

final record = AudioRecorder();
final player = AudioPlayer();

enum OperationLabel {
  flipAudio('Flip Audio', 'flip-audio'),
  toSine('To Sine', 'to-sine');

  const OperationLabel(this.label, this.endpoint);
  final String label;
  final String endpoint;
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  bool isRecording = false;
  bool isPlaying = false;

  final TextEditingController operationController = TextEditingController();
  OperationLabel? selectedOperation;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: <Widget>[
          // LOGO ROW
          const Expanded(
            child: Center(
              child: Image(
                image: AssetImage('assets/images/sonic-eye-logo.png'),
                width: 100,
              ),
            ),
          ),

          // GENERATION OPTIONS
          Expanded(
            flex: 4,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                // Audio operation dropdown
                DropdownMenu<OperationLabel>(
                  initialSelection: OperationLabel.flipAudio,
                  controller: operationController,
                  requestFocusOnTap: true,
                  label: const Text('Operation', style: TextStyle(color: Colors.white)),
                  textStyle: const TextStyle(
                    color: Colors.white,
                  ),
                  trailingIcon: const Icon(
                    Icons.arrow_drop_down,
                    color: Colors.white,
                  ),
                  selectedTrailingIcon: const Icon(
                    Icons.arrow_drop_up,
                    color: Colors.white,
                  ),
                  onSelected: (OperationLabel? operation) {
                    setState(() {
                      selectedOperation = operation;
                    });
                  },
                  dropdownMenuEntries: OperationLabel.values
                      .map<DropdownMenuEntry<OperationLabel>>(
                          (OperationLabel operation) {
                    return DropdownMenuEntry<OperationLabel>(
                      value: operation,
                      label: operation.label,
                    );
                  }).toList(),
                ),
              ],
            ),
          ),

          Expanded(
            // ACTION BUTTONS
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: <Widget>[
                // Record button
                ElevatedButton(
                  
                  onPressed: true ? null : () {
                    isRecording ? stopRecording() : startRecording();
                    setState(() {
                      isRecording = !isRecording;
                    });
                  },
                  style: ElevatedButton.styleFrom(
                    shape: const CircleBorder(),
                    minimumSize: const Size(75, 75),
                    backgroundColor: isRecording ? Colors.red : Colors.blue[600],
                  ),
                  child: isRecording ?
                    const Icon(Icons.square, color: Colors.white, size: 30) :
                    const Icon(Icons.mic, color: Colors.white, size: 30),
                ),

                // Generate button
                ElevatedButton(
                  onPressed: () {
                    generateAudio(selectedOperation);
                  },
                  style: ElevatedButton.styleFrom(
                    shape: const CircleBorder(),
                    minimumSize: const Size(75, 75),
                    backgroundColor: Colors.cyan[300],
                  ),
                  child: const Icon(Icons.multitrack_audio_rounded, color: Colors.white, size: 30),
                ),

                // Save button
                ElevatedButton(
                  onPressed: () {
                    // IMPLEMENT SAVE FUNCTIONALITY
                    print('Save button pressed');
                  },
                  style: ElevatedButton.styleFrom(
                    shape: const CircleBorder(),
                    minimumSize: const Size(75, 75),
                    backgroundColor: Colors.blue[600],
                  ),
                  child: const Icon(Icons.save, color: Colors.white, size: 30),
                ),
              ],
            ),
          ),

          const Expanded(
            // PLAY AUDIO & SLIDER
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: <Widget>[
                const AudioController(),
                // IMPLEMENT AUDIO PLAYBACK SLIDER
              ],
            ),
          ),
        ],
      ),
    );
  }
}

void startRecording() async {
  // Check and request permission if needed
  if (await record.hasPermission()) {
    // Start recording to file
    Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
    String filePath = '${appDocumentsDirectory.path}/test.wav';
    await record.start(const RecordConfig(encoder: AudioEncoder.wav),
        path: filePath);
  }
}

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

void stopRecording() async {
  await record.stop();
}

void deleteRecording() async {
  record.dispose();
}

void generateAudio(OperationLabel? operation) async {
  showDebugToast('Sending audio to server');

  String resultUri = await sendRecording(operation ?? OperationLabel.flipAudio);

  if(resultUri.isEmpty) {
    showDebugToast('Failed to receive response from server', Colors.red);
  } else {
    showDebugToast('Received response from server, downloading audio');

    try {
      // TODO: Verify received URI before downloading
      bool downloadSuccessful = await downloadRecording(resultUri);
      if(downloadSuccessful) {
        showDebugToast('Audio successfully downloaded!');
      } else {
        showDebugToast('Failed to download audio from server', Colors.red);
      }
    } catch (error) {
      showDebugToast('Failed to download audio from server', Colors.red);
    }
  }
}

Future<String> sendRecording(OperationLabel operation) async {
  // Define paths
  var url = Uri.http('192.168.166.156:5000', 'api/${operation.endpoint}');
  Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
  String filePath = '${appDocumentsDirectory.path}/test.wav';

  // Prepare request
  Dio dio = Dio();
  dio.options.headers['Connection'] = 'Keep-Alive';
  dio.options.contentType = 'multipart/form-data';
  dio.options.connectTimeout = const Duration(seconds: 30);
  FormData formData = FormData.fromMap({
    'audio': await MultipartFile.fromFile(filePath, filename: 'test.wav'),
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
  // Define local file path
  Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
  String filePath = '${appDocumentsDirectory.path}/audio.wav';

  // Prepare request
  Dio dio = Dio();
  dio.options.headers['Connection'] = 'Keep-Alive';
  dio.options.connectTimeout = const Duration(seconds: 30);

  // Send request
  var response = await dio.download(url, filePath);
  
  return response.statusCode == 200;
}

void playRecording(AudioPlayer player) async {
  // Define local file path
  Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
  String filePath = '${appDocumentsDirectory.path}/audio.wav';
  try {
    player.play(DeviceFileSource(filePath));
  } catch (error) {
    print('Error: $error');
    showDebugToast('Failed to find audio file', Colors.red);
  }
}