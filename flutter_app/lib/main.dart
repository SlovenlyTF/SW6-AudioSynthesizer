import 'package:flutter/material.dart';
import 'pages/home.dart';

void main() {
  runApp(const MyApp());
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
      theme: ThemeData.from(colorScheme: sonicColorSchemeDark),
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
  static const TextStyle optionStyle =
      TextStyle(fontSize: 30, fontWeight: FontWeight.bold);
  static const List<Widget> _widgetOptions = <Widget>[
    HomePage(),
    // TODO: Implement archive page
    Text(
      'Index 1: Archive',
      style: optionStyle,
    ),
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
