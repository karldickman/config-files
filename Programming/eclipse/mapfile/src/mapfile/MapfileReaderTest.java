package mapfile;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import org.junit.Test;

public class MapfileReaderTest {

	MapfileReader reader;
	Scanner scanner;

	@Test
	public void read() throws ReadError, FileNotFoundException {
		scanner = new Scanner(
				"thing: stuff#comment\n#comment\nyour: mom\nsucks: xkcd");
		reader = new MapfileReader(scanner);
		Map<String, String> wanted = new HashMap<String, String>();
		wanted.put("thing", "stuff");
		wanted.put("your", "mom");
		wanted.put("sucks", "xkcd");
		assertTrue(wanted.equals(reader.read()));
	}

	@Test
	public void mergeLines() throws ReadError {
		String[][] sources = new String[][] { { "thing", "stuff" },
				{ "thing", "\tstuff" }, { "thing", "", "", "", "stuff" },
				{ "thing", " ", "stuff" }, { "thing", "", " ", "", "stuff" },
				{ "thing", " stuff", "your", " mom" },
				{ "thing", "stuff", " mom", "item" } };
		String[][] wanteds = new String[][] { { "thing", "stuff" },
				{ "thing\tstuff" }, { "thing", "stuff" }, { "thing", "stuff" },
				{ "thing", "stuff" }, { "thing stuff", "your mom" },
				{ "thing", "stuff mom", "item" }, };
		for (int i = 0; i < sources.length; i++) {
			String[] result = MapfileReader.mergeLines(sources[i]);
			assertEquals(wanteds[i].length, result.length);
			for (int j = 0; j < wanteds[i].length; j++) {
				assertTrue(wanteds[i][j].equals(result[j]));
			}
		}
		try {
			MapfileReader.mergeLines(new String[] { "  thing", "stuff" });
			fail("This shouldn't parse.");
		} catch (ReadError error) {

		}
	}

	@Test
	public void pairify() throws ReadError {
		String[] sources = new String[] { "blank:   \t  ", "key:  value ",
				"key :  x:k:c: d  " };
		String[][] wanteds = new String[][] { { "blank", "" },
				{ "key", "value" }, { "key", "x:k:c: d" } };
		for (int i = 0; i < sources.length; i++) {
			String[] result = MapfileReader.pairify(sources[i]);
			assertTrue(wanteds[i][0].equals(result[0]));
			assertTrue(wanteds[i][1].equals(result[1]));
		}
		try {
			MapfileReader.pairify("thing");
			fail("pairify(\"thing\") should raise a ParseError.");
		} catch (ReadError error) {
		}
	}

	@Test
	public void pairs() throws ReadError {
		String[] source = { "sucks: xkcd", "thing: stuff  ", "your:  \tmom" };
		Map<String, String> wanted = new HashMap<String, String>();
		wanted.put("thing", "stuff");
		wanted.put("your", "mom");
		wanted.put("sucks", "xkcd");
		assertTrue(wanted.equals(MapfileReader.pairs(Arrays.asList(source))));
	}

	@Test
	public void removeComments() {
		String[][] sources = { { "not a comment", "  #a comment" },
				{ "not a comment#acomment" },
				{ "not a comment", "#a comment", "not a comment" },
				{ "not a comment\\#not a comment either" } };
		String[][] wanteds = { { "not a comment" }, { "not a comment" },
				{ "not a comment", "not a comment" },
				{ "not a comment\\#not a comment either" } };
		for (int i = 0; i < sources.length; i++) {
			List<String> result = MapfileReader.removeComments(sources[i]);
			assertEquals(wanteds[i].length, result.size());
			for (int j = 0; j < wanteds[i].length; j++) {
				assertTrue(wanteds[i][j].equals(result.get(j)));
			}
		}
	}

	@Test
	public void startsWithWhitespace() {
		assertTrue(MapfileReader.startsWithWhitespace(""));
		assertTrue(MapfileReader.startsWithWhitespace("  "));
		assertTrue(MapfileReader.startsWithWhitespace("\t"));
		assertTrue(MapfileReader.startsWithWhitespace("\tstuff"));
		assertFalse(MapfileReader.startsWithWhitespace("thing"));
	}
}
