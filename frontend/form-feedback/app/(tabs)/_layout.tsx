import { Tabs } from 'expo-router';
import { Dimensions } from 'react-native';

const deviceHeight = Dimensions.get('window').height;
const deviceWidth = Dimensions.get('window').width;
const deviceMinDimension = Math.min(deviceWidth, deviceHeight);

export default function TabsLayout() {
    return (
        <Tabs
            screenOptions={{
                tabBarActiveTintColor: '#111',
                tabBarInactiveTintColor: '#888',
                tabBarIconStyle: { display: 'none' },
                tabBarLabelStyle: {
                    fontSize: deviceHeight * 0.02,
                },
            }}
        >
            <Tabs.Screen
                name="index"
                options={{
                    title: 'Home',
                }}
            />
            <Tabs.Screen
                name="history"
                options={{
                    title: 'History',
                }}
            />
        </Tabs>
    );
}
