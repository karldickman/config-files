package mapfile;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class MapfileReader {

	/** Merge all logical lines into physical lines. */
	protected static String[] mergeLines(String[] oldLines) throws ReadError {
		String[] lines = new String[oldLines.length];
		int i, lineIndex = 0, offset;
		for (offset = 0; offset < oldLines.length; offset++) {
			if (oldLines[offset].length() > 0
					&& !oldLines[offset].matches("^\\s*$")) {
				break;
			}
		}
		if (startsWithWhitespace(oldLines[offset])) {
			throw (new ReadError(offset + ": '" + oldLines[offset]
					+ ": Keys cannot be indented."));
		}
		for (i = offset; i < oldLines.length; i++) {
			String line = oldLines[i];
			if (startsWithWhitespace(line)) {
				lines[lineIndex - 1] += line;
			} else {
				lines[lineIndex] = line;
				lineIndex++;
			}
		}
		String[] newLines = new String[lineIndex];
		for (i = 0; i < lineIndex; i++) {
			newLines[i] = lines[i].trim();
		}
		return newLines;
	}

	/** Turn a line into a key-value pair. */
	protected static String[] pairify(String line) throws ReadError {
		String[] items = line.split(":", 2);
		try {
			items[0] = items[0].trim();
			items[1] = items[1].trim();
		} catch (ArrayIndexOutOfBoundsException error) {
			throw (new ReadError("'" + line
					+ "': Keys must be terminated with a colon."));
		}
		return items;
	}

	/** Parse the lines into a map of key/value pairs. */
	protected static Map<String, String> pairs(Collection<String> lines)
			throws ReadError {
		Map<String, String> result = new HashMap<String, String>();
		for (String line : lines) {
			String[] items = pairify(line);
			result.put(items[0], items[1]);
		}
		return result;
	}

	/** Remove all comments. */
	protected static List<String> removeComments(String[] oldLines) {
		List<String> lines = new LinkedList<String>();
		for (int i = 0; i < oldLines.length; i++) {
			if (oldLines[i].matches("^\\s*#.*$")) {
			} else if (oldLines[i].matches("^.*[^\\\\]#.*$")) {
				lines.add(oldLines[i].replaceAll("(?<!\\\\)#.*$", ""));
			} else {
				lines.add(oldLines[i]);
			}
		}
		return lines;

	}

	/** Check if a line starts with whitespace. */
	protected static boolean startsWithWhitespace(String line) {
		if (line.length() == 0) {
			return true;
		}
		return line.matches("^\\s+.*");
	}

	/** The file to be read. */
	private Scanner scanner;

	public MapfileReader(String fileName) throws FileNotFoundException {
		this(new File(fileName));
	}

	public MapfileReader(File file) throws FileNotFoundException {
		this(new Scanner(file));
	}

	protected MapfileReader(Scanner scanner) throws FileNotFoundException {
		this.scanner = scanner;
	}

	/** Parse the file into a list of key value pairs. */
	public Map<String, String> read() throws ReadError {
		List<String> lines = new ArrayList<String>();
		while (scanner.hasNextLine()) {
			lines.add(scanner.nextLine());
		}
		String[] arrLines = new String[lines.size()];
		for (int i = 0; i < lines.size(); i++) {
			arrLines[i] = lines.get(i);
		}
		return pairs(removeComments(mergeLines(arrLines)));
	}

}
