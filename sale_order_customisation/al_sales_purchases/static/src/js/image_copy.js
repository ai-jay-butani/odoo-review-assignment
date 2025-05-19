/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ImageField } from "@web/views/fields/image/image_field";

export class PatchedImageField extends ImageField{
        async copyImageToClipboard(ev) {
            ev.preventDefault();
            try {
                const blob = await (await window.fetch(this.getUrl(this.props.name))).blob();

                // Convert blob to Image element
                const img = new Image();
                img.crossOrigin = "anonymous"; // Required to avoid tainted canvas
                img.src = URL.createObjectURL(blob);

                img.onload = async () => {
                    // Draw to canvas
                    const canvas = document.createElement("canvas");
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext("2d");
                    ctx.drawImage(img, 0, 0);

                    // Convert canvas to PNG blob
                    canvas.toBlob(async (pngBlob) => {
                        try {
                            await navigator.clipboard.write([
                                new ClipboardItem({ "image/png": pngBlob })
                            ]);
                            this.notification.add("Image copied to clipboard!", {type: "success"});
                        } catch (err) {
                            console.error("Clipboard write failed:", err);
                            this.notification.add("Clipboard write failed.", {type: "danger"});
                        }
                    }, "image/png");
                };

                img.onerror = () => {
                    this.notification.add("Failed to load image into canvas.", {type: "danger"});
                };

            } catch (err) {
                this.notification.add("Failed to copy image.", {type: "danger"});
            }
        }
}

const imageField = registry.category("fields").get("image");

imageField.component = PatchedImageField;
