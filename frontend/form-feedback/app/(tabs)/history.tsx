import { Dimensions, FlatList, StyleSheet, Text, View } from 'react-native';

const deviceHeight = Dimensions.get('window').height;
const deviceWidth = Dimensions.get('window').width;
const deviceMinDimension = Math.min(deviceWidth, deviceHeight);

const history = [
    "Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat.",
    "Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas.",
    "Iaculis massa nisl malesuada lacinia integer nunc posuere.",
];

export default function ResultsScreen() {
    return (
        <View style={styles.container}>
            <FlatList
                data={history}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => (
                    <View style={styles.listItem}>
                        <Text style={styles.itemText}>{item}</Text>
                    </View>
                )}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        backgroundColor: '#FFF',
    },
    listItem: {
        padding: 15,
        backgroundColor: '#eee',
        borderBottomWidth: 1,
        borderBottomColor: '#ccc',
        marginBottom: 5,
        borderRadius: 5,
    },
    itemText: {
        fontSize: deviceMinDimension * 0.04
    },
});
