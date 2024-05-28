import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_app/states/archive_delete_notifier.dart';
import 'package:flutter_app/states/archive_player_notifier.dart';
import 'package:flutter_app/utilities/file_system.dart';
import 'package:flutter_app/widgets/archive_audio_controller.dart';
import 'package:flutter_app/widgets/delete_button.dart';
import 'package:flutter_app/widgets/share_button.dart';
import 'package:provider/provider.dart';
import 'package:accordion/accordion.dart';

class ArchivePage extends StatefulWidget {
  const ArchivePage({super.key});

  @override
  State<ArchivePage> createState() => _ArchivePageState();
}

class _ArchivePageState extends State<ArchivePage> {

  late List<String> audioFilePaths;
  late bool isLoading = true;

  @override
  void initState() {
    super.initState();
    audioFilesList().then((files) {
      setState(() {
        audioFilePaths = files.reversed.toList();
        isLoading = false;
      });
    });
  }

  Future<List<String>> audioFilesList() async {
    String archivePath = await getArchivePath();
    Directory archiveDirectory = Directory(archivePath);
    List<String> files = [];
    if (archiveDirectory.existsSync()) {
      files = archiveDirectory.listSync().map((file) => file.path).toList();
    }
    return files;
  }

  void removeItem(int index) {
    setState(() {
      audioFilePaths.removeAt(index);
    });
  }
  
  ArchiveAudioController displayAudioController(int index) {
    String path = audioFilePaths[index];
    String fileName = path.substring(path.lastIndexOf('/') + 1);
    return ArchiveAudioController(
      index: index,
      filePath: Future.value(path), 
      playerTitle: Future.value(fileName),
      canPlay: true,
    );
  }

  void pageTapped(context) {
    // Reset active index to deselect any active buttons
    Provider.of<ArchiveDeleteNotifier>(context, listen: false).setActiveIndex(-1);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ChangeNotifierProvider<ArchiveDeleteNotifier>(
        create: (context) => ArchiveDeleteNotifier(),
        // Wrapping with builder to create new context
        child: Builder(
          builder: (BuildContext context) => GestureDetector(
            onTap: () => pageTapped(context),
            child: Center(
              child: isLoading 
              ? const CircularProgressIndicator() 
              : Padding(
                  padding: const EdgeInsets.only(top: 10),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      audioFilePaths.isNotEmpty ? Expanded(
                        child: SingleChildScrollView(
                            child: ChangeNotifierProvider<ArchivePlayerNotifier>(
                              create: (context) => ArchivePlayerNotifier(),
                              child: Accordion(
                                disableScrolling: true,
                                headerBackgroundColor: const Color.fromARGB(255, 7, 37, 80),
                                contentBackgroundColor: const Color.fromARGB(255, 7, 37, 80),
                                contentBorderWidth: 0,
                                scaleWhenAnimating: false,
                                children: audioFilePaths.map((path) {
                                  int index = audioFilePaths.indexOf(path);
                                  return AccordionSection(
                                    header: displayAudioController(index),
                                    content: Row(
                                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                      children: [
                                        ShareButton(filePath: audioFilePaths[index]),
                                        DeleteButton(
                                          index: index,
                                          filePath: audioFilePaths[index],
                                          onDelete: () => removeItem(index)
                                        ),
                                      ],
                                    ),
                                  );
                                }).toList(),
                              )
                            )
                          ),
                      ) : const Padding(
                        padding: EdgeInsets.all(24.0),
                        child: Text(
                          '🤔 No audio files saved in the archive.',
                          style: TextStyle(fontSize: 24, color: Colors.white),
                          textAlign: TextAlign.center,
                        ),
                      ),
                    ]
                  ),
                ),
            ),
          ),
        ),
      ),
    );
  }

}