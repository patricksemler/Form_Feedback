import { View, Text, StyleSheet } from 'react-native';

export default function ResultsScreen() {
    return (
        <View style={styles.container}>
            <Text style={styles.title}>📊 History</Text>
            <Text style={styles.paragraph}>(stuff here)</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    paragraph: {
        fontSize: 18,
        marginBottom: 10,
    },
});
