function (doc) {
  if (doc.type == "operator") {
    emit(doc.callsign, doc._id);
  }
}
