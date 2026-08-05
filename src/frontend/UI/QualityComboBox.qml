import QtQuick
import QtQuick.Controls

ComboBox {
    id: control

    // Public Properties mapping to your Python arguments
    property var availableHeights: []
    property var preferredQuality: "best"
    property bool hasLicense: false

    // Equivalent to your FREE_MAX_HEIGHT and LOCKED_LABELS
    readonly property int freeMaxHeight: 720
    readonly property var lockedLabels: ["best", "half", "worst"]

    // Used to match PySide _longest_item_width_px()
    property int _maxPopupWidth: 0

    // Qt 6 supports valueRole, letting us bind complex data directly
    textRole: "text"
    valueRole: "value"
    model: ListModel { id: internalModel }

    // TextMetrics replaces PySide's QFontMetrics
    TextMetrics {
        id: textMetrics
        font: control.font
    }

    // Custom delegate to handle enabled/disabled states (the license check)
    delegate: ItemDelegate {
        width: control.popup.width
        text: model.text
        enabled: model.isItemEnabled
        highlighted: control.highlightedIndex === index

        contentItem: Text {
            text: parent.text
            font: control.font
            // Use system palette for dark/light mode support
            color: parent.enabled ? (parent.highlighted ? control.palette.highlightedText : control.palette.text)
                                  : control.palette.placeholderText // Grayed out if no license
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }
    }

    // Equivalent to fit_combo_popup()
    popup: Popup {
        y: control.height - 1
        // Auto-size: Never smaller than control, but expands to widest text
        width: Math.max(control.width, control._maxPopupWidth)
        implicitHeight: contentItem.implicitHeight
        padding: 1

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex
            ScrollIndicator.vertical: ScrollIndicator { }
        }
    }

    // Rebuild data whenever inputs change
    onAvailableHeightsChanged: rebuildModel()
    onPreferredQualityChanged: rebuildModel()
    onHasLicenseChanged: rebuildModel()

    Component.onCompleted: rebuildModel()

    // JS equivalent of your 4 Python data/logic functions
    function rebuildModel() {
        // 1. Normalize & Sort heights (worst->best)
        let heights = [];
        if (availableHeights) {
            // Remove duplicates and nulls, sort descending (best to worst)
            let uniqueHeights = Array.from(new Set(availableHeights)).filter(h => h !== null);
            heights = uniqueHeights.sort((a, b) => b - a);
        }

        // Helper equivalent to apply_license_state_quality_combo() inner loop
        function checkEnabled(val) {
            if (hasLicense) return true;
            if (typeof val === "string" && lockedLabels.includes(val.toLowerCase())) return false;
            if (typeof val === "number" && val > freeMaxHeight) return false;
            return true;
        }

        let newItems = [];

        // 2. Add auto labels
        newItems.push({ text: "Best", value: "best", isItemEnabled: checkEnabled("best") });
        newItems.push({ text: "Half", value: "half", isItemEnabled: checkEnabled("half") });
        newItems.push({ text: "Worst", value: "worst", isItemEnabled: checkEnabled("worst") });

        // 3. Add numeric heights
        for (let i = 0; i < heights.length; i++) {
            let h = heights[i];
            newItems.push({ text: h + "p", value: h, isItemEnabled: checkEnabled(h) });
        }

        // Update the actual ListModel
        internalModel.clear();
        let maxTextW = 0;

        for (let i = 0; i < newItems.length; i++) {
            internalModel.append(newItems[i]);

            // Measure text width for fit_combo_popup equivalent
            textMetrics.text = newItems[i].text;
            if (textMetrics.width > maxTextW) {
                maxTextW = textMetrics.width;
            }
        }

        // Add padding + indicator space to max text width
        _maxPopupWidth = maxTextW + 40;

        // 4. Determine Default Value (Equivalent to _choose_default_quality_value)
        let targetValue = preferredQuality;

        // Force down to 720 if unlicensed
        if (!hasLicense) {
            if (typeof targetValue === "string" && lockedLabels.includes(targetValue.toLowerCase())) {
                targetValue = freeMaxHeight;
            }
            if (typeof targetValue === "number" && targetValue > freeMaxHeight) {
                targetValue = freeMaxHeight;
            }
        }

        let bestIdx = -1;

        // Try exact match
        for (let i = 0; i < newItems.length; i++) {
            if (newItems[i].value === targetValue && newItems[i].isItemEnabled) {
                bestIdx = i;
                break;
            }
        }

        // If numeric and no exact match, find closest allowed height
        if (bestIdx === -1 && heights.length > 0) {
            let targetNum = parseInt(targetValue);
            if (isNaN(targetNum)) targetNum = freeMaxHeight;

            let below = heights.filter(h => h <= targetNum && checkEnabled(h));
            let chosenHeight = null;

            if (below.length > 0) {
                chosenHeight = Math.max(...below); // Highest <= target
            } else {
                // Absolute closest fallback
                let available = heights.filter(h => checkEnabled(h));
                if (available.length > 0) {
                    chosenHeight = available.reduce((prev, curr) =>
                        Math.abs(curr - targetNum) < Math.abs(prev - targetNum) ? curr : prev
                    );
                }
            }

            if (chosenHeight !== null) {
                for (let i = 0; i < newItems.length; i++) {
                    if (newItems[i].value === chosenHeight && newItems[i].isItemEnabled) {
                        bestIdx = i;
                        break;
                    }
                }
            }
        }

        // _set_combo_to_value_first_enabled Fallback
        if (bestIdx === -1) {
            for (let i = 0; i < newItems.length; i++) {
                if (newItems[i].isItemEnabled) {
                    bestIdx = i;
                    break;
                }
            }
        }

        // Apply index
        control.currentIndex = Math.max(0, bestIdx);
    }
}