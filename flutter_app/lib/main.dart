import 'dart:collection';

import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:dio/dio.dart';

final record = AudioRecorder();

void main() {
  runApp(const MyApp());
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

  @override Widget build(BuildContext context) {
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
                    isRecording ? stopRecording() : startRecording();
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
                )
              ),
            ),
          ),
          const Divider( // Horizontal divider
            thickness: 5,
            color: Colors.black,
          ),
          // Second half of the screen
          Expanded(
            flex: 1,
            child: Container(
              child: Center(
                child: TextButton.icon(
                  onPressed: () {
                    stopRecording();
                  }, 
                  icon: Icon(Icons.play_arrow),
                  label: Text('Play'),
                )
              ),
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
    await record.start(const RecordConfig(encoder: AudioEncoder.wav), path: filePath);
  }
}

void stopRecording() async {
  await record.stop();
  //sendRecording();
  downloadRecording();
  print('fuck you');
}

void deleteRecording() async {
  record.dispose();
}

void sendRecording() async {
  var url = Uri.http('10.0.2.2:5000', 'flip_audio');
  Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
  String filePath = '${appDocumentsDirectory.path}/test.wav';
  Dio dio = Dio();
  dio.options.headers['Connection'] = 'Keep-Alive';
  dio.options.connectTimeout = Duration(seconds: 30);
  FormData formData = FormData.fromMap({
    'audio': await MultipartFile.fromFile(filePath, filename: 'test.wav'),
  });
  try {
    var response = await dio.post(url.toString(), data: formData);
    print(response.statusCode);
  } catch (e) {
    print('Error: $e');
  }
}

Future<Response> downloadRecording() async {
  var url = Uri.http('10.0.2.2:5000', 'host_audio');
  Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
  String filePath = '${appDocumentsDirectory.path}/audio.wav';
  Dio dio = Dio();
  dio.options.headers['Connection'] = 'Keep-Alive';
  //dio.options.responseType = ResponseType.bytes;
  dio.options.connectTimeout = Duration(seconds: 30);
  dio.interceptors.add(LogInterceptor(responseBody: true, logPrint: (o) => debugPrint(o.toString())));
  var response = await dio.download(url.toString(), filePath);
  print('HELLLLOOOOOO: ' + response.data.toString());
  return response;
}