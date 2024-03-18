import 'dart:collection';

import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:dio/dio.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:fluttertoast/fluttertoast.dart';

final record = AudioRecorder();

void main() {
  runApp(const MyApp());
}

enum OperationLabel {
  flipAudio('Flip Audio', 'flip-audio'),
  toSine('To Sine', 'to-sine');

  const OperationLabel(this.label, this.endpoint);
  final String label;
  final String endpoint;
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // TRY THIS: Try running your application with "flutter run". You'll see
        // the application has a purple toolbar. Then, without quitting the app,
        // try changing the seedColor in the colorScheme below to Colors.green
        // and then invoke "hot reload" (save your changes or press the "hot
        // reload" button in a Flutter-supported IDE, or press "r" if you used
        // the command line to start the app).
        //
        // Notice that the counter didn't reset back to zero; the application
        // state is not lost during the reload. To reset the state, use hot
        // restart instead.
        //
        // This works for code too, not just values: Most code changes can be
        // tested with just a hot reload.
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'On THAT Note...'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool isRecording = false;

  final TextEditingController operationController = TextEditingController();
  OperationLabel? selectedOperation;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Column(
        children: <Widget>[
          // First half of the screen
          Expanded(
            flex: 1,
            child: Container(
              child: Center(
                  child: TextButton.icon(
                onPressed: () {
                  isRecording
                      ? stopRecording(selectedOperation)
                      : startRecording();
                  setState(() {
                    isRecording = !isRecording;
                  });
                },
                icon: Icon(Icons.mic),
                label: Text('Record'),
                style: ButtonStyle(
                  backgroundColor: MaterialStateProperty.all<Color>(
                    isRecording ? Colors.red : Colors.blue,
                  ),
                ),
              )),
            ),
          ),
          // Audio operation dropdown
          DropdownMenu<OperationLabel>(
            initialSelection: OperationLabel.flipAudio,
            controller: operationController,
            // requestFocusOnTap is enabled/disabled by platforms when it is null.
            // On mobile platforms, this is false by default. Setting this to true will
            // trigger focus request on the text field and virtual keyboard will appear
            // afterward. On desktop platforms however, this defaults to true.
            requestFocusOnTap: true,
            label: const Text('Operation'),
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
          const Divider(
            // Horizontal divider
            thickness: 5,
            color: Colors.black,
          ),
          // Second half of the screen
          Expanded(
            flex: 1,
            child: Center(
                child: TextButton.icon(
              onPressed: () {
                playRecording();
              },
              icon: const Icon(Icons.play_arrow),
              label: const Text('Play'),
            )),
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

void stopRecording(OperationLabel? operation) async {
  await record.stop();
  //sendRecording();

  showDebugToast('Stopped recording, sending to server');

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

void deleteRecording() async {
  record.dispose();
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

void playRecording() async {
  // Define local file path
  Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
  String filePath = '${appDocumentsDirectory.path}/audio.wav';

  AudioPlayer player = AudioPlayer();
  try {
    player.play(DeviceFileSource(filePath));
  } catch (error) {
    print('Error: $error');
    showDebugToast('Failed to find audio file', Colors.red);
  }
}
