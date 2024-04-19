import 'package:flutter/material.dart';
import 'package:flutter_app/states/generation_option_state.dart';
import 'package:flutter_app/widgets/generate_button.dart';
import 'package:flutter_app/widgets/home_audio_controller.dart';
import 'package:flutter_app/widgets/operation_dropdown.dart';
import 'package:flutter_app/widgets/record_button.dart';
import 'package:flutter_app/widgets/save_button.dart';
import 'package:provider/provider.dart';
import 'package:flutter_app/states/generation_state.dart';
import 'package:flutter_app/states/recording_state.dart';
import 'package:flutter_app/utilities/file_system.dart';
import 'package:flutter_app/states/audio_saved_state.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
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
        ChangeNotifierProvider<AudioSavedState>(
          create: (context) => AudioSavedState(),
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
      
            const Expanded(
              // ACTION BUTTONS
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  RecordButton(),
                  GenerateButton(),
                  SaveButton(),
                ],
              ),
            ),
      
            Expanded(
              // AUDIO CONTROLS
              child: HomeAudioController(filePath: getTempGeneratedPath()),
            ),
          ],
        ),
      ),
    );
  }
}
