import 'dart:io';
import 'package:path_provider/path_provider.dart';

// TODO: Probably more appropriate to provide these through a state?

Future<String> getTempRecordingPath() async {
  Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
  return '${appDocumentsDirectory.path}/ephemeral_recording.wav';
}

Future<String> getTempGeneratedPath() async {
  Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
  return '${appDocumentsDirectory.path}/ephemeral_generated.wav';
}

Future<String> getArchivePath() async {
  Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
  return '${appDocumentsDirectory.path}/archive';
}