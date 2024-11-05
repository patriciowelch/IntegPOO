package cliente.code.headers;

import javax.swing.text.*;

public class NumericTextFieldFilter extends DocumentFilter {

    @Override
    public void insertString(FilterBypass fb, int offset, String string, AttributeSet attr) throws BadLocationException {
        if (isValidInput(string, fb.getDocument().getText(0, fb.getDocument().getLength()))) {
            super.insertString(fb, offset, string, attr);
        }
    }

    @Override
    public void replace(FilterBypass fb, int offset, int length, String text, AttributeSet attrs) throws BadLocationException {
        if (isValidInput(text, fb.getDocument().getText(0, fb.getDocument().getLength()))) {
            super.replace(fb, offset, length, text, attrs);
        }
    }

    private boolean isValidInput(String input, String currentText) {
        String newText = currentText + input;

        // Permitir números negativos y decimales
        return newText.matches("-?\\d*(\\.\\d*)?");
    }
}

