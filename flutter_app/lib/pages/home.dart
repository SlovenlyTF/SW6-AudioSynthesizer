import 'package:flutter/material.dart';
import 'package:flutter_app/states/generation_option_state.dart';
import 'package:flutter_app/widgets/audio_controller.dart';
import 'package:flutter_app/widgets/generate_button.dart';
import 'package:flutter_app/widgets/operation_dropdown.dart';
import 'package:flutter_app/widgets/record_button.dart';
import 'package:provider/provider.dart';
import 'package:flutter_app/states/generation_state.dart';
import 'package:flutter_app/states/recording_state.dart';
import 'package:flutter_app/utilities/file_system.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  bool isRecording = false;

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<RecordingState>(
          create: (context) => RecordingState(),
        ),
        ChangeNotifierProvider<GenerationState>(
          create: (context) => GenerationState(),
        ),
        ChangeNotifierProvider<GenerationOptionState>(
          create: (context) => GenerationOptionState(),
        ),
      ],
      child: Scaffold(
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
            const Expanded(
              flex: 4,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  // Audio operation dropdown
                  OperationDropdown(),
                ],
              ),
            ),
      
            Expanded(
              // ACTION BUTTONS
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  const RecordButton(),
                  const GenerateButton(),
      
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
      
            Expanded(
              // PLAY AUDIO & SLIDER
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  AudioController(filePath: getTempGeneratedPath()),
                  // IMPLEMENT AUDIO PLAYBACK SLIDER
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
