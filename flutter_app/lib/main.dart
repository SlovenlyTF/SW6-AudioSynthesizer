import 'dart:io';

import 'package:flutter/material.dart';
import 'pages/home.dart';
import 'pages/archive.dart';
import 'utilities/file_system.dart';
import 'package:google_fonts/google_fonts.dart';

void main() async {
  bool isInitialized = await initialize();
  if(!isInitialized) {
    print('Failed to initialize');
    return;
  }

  runApp(const MyApp());
}

Future<bool> initialize() async {
  try {
    WidgetsFlutterBinding.ensureInitialized();

    // Ensure archive directory exists
    var archivePath = await getArchivePath();
    var arciveDir = Directory(archivePath);
    if(!arciveDir.existsSync()) arciveDir.createSync();

    print('DA FING IS NAO INITIALISED MAN!!!!');
    return true;
  } catch (error) {
    print('FAILED TO INITIALIZE WITH ERROR: $error');
    return false;
  }
}

// Define your custom color scheme
const ColorScheme sonicColorSchemeDark = ColorScheme(
  primary: Color(0xFF35ACDA),
  secondary: Color(0xFF35ACDA),
  surface: Color(0xFFC4F2F0),
  background: Color(0xFF070D3A),
  error: Colors.deepOrange,
  onPrimary: Colors.white,
  onSecondary: Colors.white,
  onSurface: Colors.black,
  onBackground: Colors.white,
  onError: Colors.white,
  brightness: Brightness.dark,
);

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: sonicColorSchemeDark,
        fontFamily: GoogleFonts.dmSans().fontFamily,
      ),
      home: const MainPage(title: 'On THAT Note...'),
    );
  }
}

class MainPage extends StatefulWidget {
  const MainPage({super.key, required this.title});

  final String title;

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  // TODO: Move navbar to separate widget
  int _selectedPage = 0;
  static const List<Widget> _widgetOptions = <Widget>[
    HomePage(),
    ArchivePage(),
  ];

  void _onNavTapped(int index) {
    setState(() {
      _selectedPage = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: _widgetOptions.elementAt(_selectedPage),
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.archive),
            label: 'Archive',
          ),
        ],
        currentIndex: _selectedPage,
        onTap: _onNavTapped,
      ),
      backgroundColor: const Color.fromRGBO(7, 13, 58, 1),
    );
  }
}
